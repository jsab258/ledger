# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-19 21:37 (the hourly run; the last session set its Stopped line at 21:30)

**Row due:** by 23:16 (last row 22:16; page read 22:14)
**Stopped:** 2026-11-19 22:24 (allowance above the week's ceiling at an item's end, 53% against 52.7%: start nothing new; nothing of mine running, the heavy lock free)
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


## Done this run (21:37 on)
- Advisors 259 (licence edits wait for his message in a session he starts) and 260 (his five picks: waiting list item 29, for the order of 23 Nov) read, recorded and acked.
- Lane reports read and recorded (DECISIONS): layered3 set aside (both tries failed; 124 of 296 counted points are the jumper's own cuff fold-backs, a question for the judge after Saturday; untried next method: seams closed after the last strain-limit pass). R4 refit2 passes (Ron's back welt 1.053 on the stricter measure listed); its uncommitted work committed on lane-r4-refit2 6af953b; Kiln v1 checklist line 2 step 1 marked done.
- Kiln merge candidate 1 of 19 Nov (press da0ac0e + coat2 e6704d0) passed alone (cargo 142/142, Python, whole gate); Kiln main fast-forwarded to f72102e. Run folder runs/kiln-merge-cand-2026-11-19; worktree C:/LedgerTools/kiln-lanes/merge-cand-1119 (reuse for candidate 2).
- Ron's held rows imported into mh-assemble (RonWorkTrousers now F4-a; new RonJumperOverTrousers replacing RonJumper in -WearHeld runs); garmentsShipped=PASS. The jumper's folder needed a budget line (asset-budgets.json).
- RECIPE lines for layered and refit. Stopped after this item because the allowance passed the week's ceiling (53% against 52.7%: start nothing new).

## In flight
- Nothing of mine runs. No Kiln lane runs; the heavy lock is free. The 15:10 session's Fable lanes have all reported.

## Next, in order
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; above the ceiling start nothing new; advisor 258: keep main spend low, no Fable Kiln lane before the one-shot's end row (Sat 21 Nov).
0. Verdicts (UTC, after 2026-11-19T21:14) and advisor (after 22:00 +01:00; last ack 260). Row hourly (last 22:16).
1. After the night build: Ron's seated film from the packaged copy with -WearHeld=RonWorkTrousers,RonJumperOverTrousers (packaged-walk skill; memory tester-film-past-the-title), a fresh reviewer; it tells whether the ankle patch is the boots' missing ankle joint.
2. With room under the ceiling: merge candidate 2 (Kiln main f72102e + lane-r4-refit2 6af953b), gate1.sh copied with labels changed, alone on a quiet machine. Then Kiln v1 line 6: the skirt's close look with KILN_PRESS_FOLDS on (one back pleat turned the wrong way is its known shortfall).
3. When production/lane/parts-tree/DECISIONS-PENDING.md lands, append it to DECISIONS (advisor 257). Advisors 252/259: the licence edits to CLAUDE.md, RULINGS and the page check only when he asks in a session he starts; meanwhile decide licences by the allowlist's principles, never ask him (four licence items still open on his page: presentmon, kiln-front-end, font-pick, dinov3; close them with decisions in that session).
4. When he taps Done on marvelous-box: md_job.py --start (try 2 of 2), then one export job over the 52 .zprj (ImportZprj, then export_api.ExportPatternJSON and ExportFBX beside each), check each opens again, list in production/art/clothing/LOG.md 'Exports'; copy the kiln-md-compare-2026-11-18 projects into F:/LedgerTools/garments. Then the reference drapes (Kiln v1 line 5).
5. Blouse2's underarm (second fault) and the nylon wrist: Fable lanes only after Saturday's one-shot end row.
6. History rewrite: HELD for his word at the PC. Then: progress page published daily; DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 19 Nov 18:12: CLAUDE.md, RULINGS and page-check edits for advisor 252 refused by the unattended run's safety check (do not retry unattended).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: Marvelous bridge start 1/2 (19 Nov, four copies, his item); layered stage trace (no try); layered fix 2/2 (both failed 19 Nov: pass weighting, interleave; Fable next); trousers seat 2 tries (accepted 17:15); seated hem gap 1/2 (F5-a); coat Opus 2/2, Fable 1/2 (the 19 Nov run on the joined lane was a measurement); stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 passed at try 1 (refit2); layered3 Fable 2/2 (set aside 19 Nov); jumper import 2 (the first failed on a missing budget line); blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

