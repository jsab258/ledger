# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-19 16:51 (the hourly run; the last session set its Stopped line at 15:10)

**Row due:** by 22:29 (last row 21:29; page read 21:19)
**Stopped:** 2026-11-19 21:30 (history near its point at an item end and advisor 258's low spend; all my own jobs ended; the lock is held by the 15:10 session's last Fable lanes (layered3, R4 refit2), which end on their own: read their reports, then check for leftover runs and the lock)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace (advisor 246): 47% at 13:37, non-Fable 23.5% against the ceiling 44.8%, hard stop 75%; Fable 51%, burn it on Kiln before his reset. This week (RULINGS): eight helpers a session, Fable at max on Kiln's hardest pieces, high effort on hard code and reviews.

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
- **Fable (advisors 248, 250):** reset pressed 19 Nov; Fable at max for Kiln's hardest pieces, prototype, simulation, any Kiln fault failing two Opus tries (given problem, tries, numbers, no conclusion); his last reset untouched, never called for. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules:** F:/LedgerTools/tool-dev/LANE-RULES.md; every Kiln brief points to it.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Page read-back, daily by the session (19 Nov):** the nightly task is off since 12 Nov; once a day query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci's page-answers-fresh fails after 2 days).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.


## Done this run (16:51 on)
- Gap 15:10-16:51 fixed in fresh_gate.py.
- Advisor 248: he pressed his Fable reset before 15:29 (week 22%, Fable 0%); press item closed; week-shape fable_reset_pending false. Advisor 251: line 22% at 15:29 to 95% Mon 07:00, ceiling line+25 capped 95, hard stop 95; new work pauses at 95 until the Monday reset unless he says more (pace_line reads it). Advisor 250: his last Fable reset untouched, never call for it; allowlist item 17 (tools); line (a) HELD (licence texts add BSD-2, BSD-3, CC0, NCSA; production/licences/one-sim/README.md), told the advisor; await its reply. Advisor 249: in DECISIONS only (RULINGS at cap). All acked. Commit 053188094 pushed (checks 108/108).
- 20:56 to 21:50: lane reports read (DECISIONS); DAILY written; advisors 253-258 done and acked (pace prototype_first, progress page checked and published v47, RULINGS lines, order of 23 Nov lines); trousers F5-a set aside; jumper re-cleared and skinned.

## In flight
- Six Fable helpers of the 15:10 session (bcf2204f; still running at 17:00, their reports land as files only, nobody receives their results), all under the heavy lock (stiffness3 held it from 16:31). Read 21:10: coat2 (knee coat collar fixed, gate pass: merge candidate; donkey set aside) and stiffness3 (set aside), DECISIONS. blouse2 read 21:15 (wrists fixed behind a switch, underarm a second fault: its own lane next, DECISIONS). Press (my lane) reported 20:55, passed try 1 (lane-press da0ac0e): merge candidate. layered3 holds the lock (try 2, 20:54). (R4 refit2: KILN-LANE-R4-REFIT2-2026-11-19.md), reports due in F:/LedgerTools/tool-dev/reports unless named: layered3 (KILN-LANE-LAYERED3-2026-11-19.md), coat2 (coat collar, also the donkey jacket's fault: KILN-LANE-COAT2-2026-11-19.md), blouse2 (wrists: KILN-LANE-BLOUSE2-2026-11-19.md), stiffness3 (a third, different method: KILN-LANE-STIFFNESS3-2026-11-19.md), Ron's trousers seat (F:/LedgerTools/garments/ron/kiln-trousers-chain/chain-boots/seat-try2/REPORT.md). If the session stops before they report, the next run reads those reports, then checks for leftover runs (kiln-lanes|regression_gate|heavy*.sh) and the lock.

## Next, in order
00. Press and coat2: merge candidates on Kiln main with the full gate on a quiet machine (Opus), then the skirt looked at; one back pleat turned the wrong way is its known shortfall. Advisor 258: keep main spend low; no Fable Kiln lane before the one-shot's end row (Sat 21 Nov); the parts tree (cloud, to Fri 18:00), the lane and the one-shot (Fri 22:10 to Sat 08:00) spend first. Merges are Opus and local: only with room under the ceiling.
00b. When production/lane/parts-tree/DECISIONS-PENDING.md lands, append it to DECISIONS (advisor 257). Advisor 252 item 2 (licences never go to him): the unattended run's safety check refused the CLAUDE.md, RULINGS and page-check edits (ack says so). Do not retry in an unattended run; a session he starts may do it. Meanwhile decide licences by the allowlist's principles, never ask him. Item 1 done (allowlist 18).
0a. Ron's trousers: F4-a stays (accepted 17:15); the 5-degree try F5-a set aside 21:35 (all through counts worse, hem unchanged; DECISIONS). Jumper re-cleared 21:45 over F4-a (0 inside; jumper-clear/F4a, DECISIONS). Skinned 21:50 (jumper-clear/F4a/skinned/ron_jumper_skinned.fbx). Next: import the held row with F4-a's trousers (seat-try2/chain/F4-a/skinned/work_trousers_skinned.fbx) into C:/LedgerTools/mh-assemble (importer, Sonnet), packaged seated film; it tells whether the ankle patch is the boots' missing ankle joint.
0. Verdicts (UTC, after 2026-11-19T19:58) and advisor (after 21:20 +01:00; last ack 258). Row hourly (last 21:29; 50%, line 27.0, ceiling 52.0, Fable 46%): week, Fable, line (`python tools/pace_line.py <week> --fable <fable>`).
1. Each Fable report as it lands: a pass goes to a merge candidate on Kiln main with the full gate on a quiet machine (Opus), a fail is recorded with its numbers (tries per RULINGS 7 Nov). Spare places (up to 8): the nylon wrist on Fable, merges and gates on Opus/Sonnet.
2. When he taps Done on marvelous-box: md_job.py --start (try 2 of 2), then one export job over the 52 .zprj (ImportZprj, then export_api.ExportPatternJSON and ExportFBX beside each), check each opens again, list in production/art/clothing/LOG.md 'Exports'; copy the kiln-md-compare-2026-11-18 projects into F:/LedgerTools/garments. Then the reference drapes (Kiln v1 line 5).
3. History rewrite: HELD for his word at the PC (the 4 unstaged files and the n09-12 line's two other homes).
4. Then: wardrobe list overnight (not 01:15-04:30); progress page published daily (`python tools/progress_page.py`, publish, `--published`); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 19 Nov 18:12: CLAUDE.md, RULINGS and page-check edits for advisor 252 refused by the unattended run's safety check (do not retry unattended).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 1/2; blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

