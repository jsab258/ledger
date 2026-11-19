# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-19 05:46 (the hourly run; the 05:06 run set its Stopped line at 05:41)

**Row due:** at the next start (last row 05:07; page and advisor read 05:32: nothing new; last ack 00:54, advisor 237)
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


## Done this run (05:06 on; details in DECISIONS 05:10 on)
- Advisor 231 closed: needs_you_page.py --waiting in ci-checks and rulings-enforcers.json; no RULINGS words (4,899 of 4,900).
- Coat: on the joined lane (9a3c5a1) with KILN_SKIN_NECK_OVER_JOINT=1 it drapes to the end for the first time; fails only at the collar assembly (stand 44.8, collar 69 mm inside the neck; stretch 6.5-6.8; seams 27-36 mm open; rest p99 1.24). Same fault; its last try is Fable's, Fable at cap: set aside to Mon 13:00 or his word. Lane report, 19 Nov section.
- Ron's trousers steps 7-8 re-run on the boots drape (importer helper): all steps pass as before (9,636 triangles, flat maps none, hems clean); sitting misses the bar: body through 304 (299; was 297), cloth inside 71 (44; was 62), in the seat. Held row files NOT replaced (new fault). chain-boots/REPORT-2026-11-19.md.
- Ron's trousers M5 step 6 PASSES offline: boots proxy (Tom's n6 maker) as a Kiln collider (import_collider) beside the standard body; drape twice on main 9b5141d with KILN_LEGACY_NAMES=1, identical; 0 points inside the boots (575 bare-foot), nearest 2.6 mm; crotch layer crossings 265 (main's gate 231: known). Kiln pictures do not draw colliders. F:/LedgerTools/garments/ron/kiln-trousers-chain/boots-proxy/STEP6-BOOTS-2026-11-19.md.

## In flight at the stop
- Nothing of mine running; the heavy lock free.
- The ceiling: 37% at 05:07 under 37.2%; Fable 45% at cap. The ceiling rises about 0.9 points an hour.

## Next, in order
0. Verdicts after the last read (UTC); advisor after 2026-11-19T00:54:00+01:00 (last ack 237). Allowance, pace_line, a row.
1. Ron's trousers: the seat's sitting fit (try 1 of 2; research first: M5 method section 4, check 4, and the jeans' chain-n7 sitting fixes): body through 304 to under 299, cloth inside 71 toward 44, on chain-boots/ (skin weights or the seat zone, not the drape). The exact commands are in chain-boots/REPORT-2026-11-19.md; pose check needs --garment work_trousers. Then the held row's files on branch ron-kiln-trousers-import (STEP-I-PREPARED) from chain-boots, the import into mh-assemble; step 9 re-clear Ron's jumper; step 10 the packaged held film with the real boots.
2. Thursday's checkpoint by this evening (KILN-V1-CHECKLIST section c): which lines miss 24 Nov, for the Marvelous recommendation.
3. Marvelous before 25 Nov: Darren's nylon jacket needs a body with a head; a look by eye at the three drapes; the money DECISION item by Tue 24 Nov.
4. Fable pieces (coat collar try 2, legs, blouse, R4) wait for Fable's reset Mon 13:00; Opus only by RULINGS' tries.
5. The DAILY token file by 19:00; the P4 table.
- tools/timelog.py start "<item> ..." at every task.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 19 Nov 05:21: the trousers' boots job on Kiln main stopped at once on SetSeamlineZipper (renamed kiln_api.kiln_set_seam_zipper on 18 Nov); KILN_LEGACY_NAMES=1 runs the job unchanged.
- 19 Nov 05:20: coat on the joined lane: collar assembly inside the neck (above).
- 18 Nov 19:31: Marvelous trousers by FBX import at scale 1.0: body a tenth size. Use the .avt bodies.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 1/2; blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).
