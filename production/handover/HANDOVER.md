# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-20 09:22 (the hourly run; the last session set its Stopped line at 08:42)

**Row due:** by 10:31 (last row 09:31, doc 2026-11-20-0931-main; page read 09:23: verdicts none after 2026-11-20T06:52 UTC; advisor none after 08:45 +01:00, last ack 265)
**Stopped:** 2026-11-20 09:32 (the 09:22 run handled advisor 265: every Fable job on claude-fable-5-2; RULINGS' 8 Nov models line updated (4,900 of 4,900, wording trimmed only), token_measures --spend now prints "Helpers' models" and FABLE VERSION WRONG for older Fable (selftest 48/48), enforcers named, fins3 brief names 5.2, one DECISIONS entry, ack and row 0931 written. Allowance 72% against a 61.9% ceiling (it jumped 10 points in an hour from the one-shot restart and the cloud lane), Fable 72%: nothing started, stopped at once. Nothing running, no helpers, heavy lock free. Earlier stops: 08:42, 08:22, 08:07 all quiet; 08:01 handled advisors 263-264.)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace (advisor 246): 47% at 13:37, non-Fable 23.5% against the ceiling 44.8%, hard stop 75%; Fable 51%, burn it on Kiln before his reset. This week (RULINGS): eight helpers a session, Fable at max on Kiln's hardest pieces, high effort on hard code and reviews.

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


## Done this run (04:07 on)
- Game menu fix built and pushed (b6e9687bc). Ron's seated film: FAIL (step 1). Fins tries 1-2 failed, research, synthesis and diagnosis done, Fable brief ready (step 2). Uncommitted notes: DECISIONS (5 entries), time log, this file; commit them with the next work commit.

## Done earlier (to 03:53)
- Advisor 262 acked 01:28; night walk diagnosed; daily page read-back done. The skirt's fins measured by pleat_flat.py (research: tool-dev/reports/RESEARCH-PLEATS-LIE-FLAT-2026-11-20.md).

## In flight
- Nothing of mine runs; no helpers; the heavy lock is free. Three old bash wait loops (17, 19 Nov) linger, harmless; ending them was refused.

## Next, in order
00. Allowance first: `python tools/pace_line.py <week> --fable <fable>`; above the ceiling start nothing new; advisor 258: keep main spend low, no Fable Kiln lane before the one-shot's end row (Sat 21 Nov).
0. Verdicts (UTC, after 2026-11-20T06:52) and advisor (after 07:55 +01:00; last acks 263, 264). Row hourly (one is due by 08:56). When he taps Done on licence-rule-2026-11-20 and his session applies advisor 259, close it (needs_you_page.py --close) and the four licence items with decisions.
0a. The one-shot (cloud) builds from 07:58 to about 18:00; its end row lifts the Fable hold: then steps 1, 2 and 5 below start.
0b. The night walk of 20 Nov quit at the title (production/audits/night-walk-2026-11-20-diagnosis.md). Tester guard in play.py (02:20) and the game fix (try 1 of 2: a menu choice takes focus only from a pointer that moved) built, committed b6e9687bc and pushed 04:40. Tonight's packaged walk proves both: read its report in the morning.
1. Ron's seated film from the packaged copy DONE 04:52: FAIL, skin in the right hem-boot gap, larger than 19 Nov (DECISIONS 04:52; switches -SitProof -MickeysInside -IdleFilm=<dir> -IdleFilmWho=Ron -WearHeld=...; without -SitProof he stands in the street). Trousers stay held; seated hem cover try 2 of 2 goes into the legs' Fable lane after Saturday's end row, this film its acceptance view.
2. Kiln v1 line 6, the fins: lane fins CLOSED 2 of 2 (4d2d608 bending band, a50e80d per-fabric thickness). Diagnosis done 06:58 (tool-dev/reports/KILN-FINS-DIAGNOSIS-2026-11-20.md): outcome A, the job's 160-degree fold angle holds the leaves; at 179 they lie down (3 of 16 pass, gap 0.9/0.3 mm) but self crossings 21 to 2138. Try 3 (the RULINGS 7 Nov different method, no yes needed): within-piece contact plus the fold angle as job data, brief READY at tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md; start one Fable helper at max the moment Saturday's one-shot end row is on the page. Lesson: test a diagnosis with one run before building a try on it.
4. Advisors 252/259: the licence edits to CLAUDE.md, RULINGS and the page check only when he asks in a session he starts; meanwhile decide licences by the allowlist's principles, never ask him (four licence items still open on his page: presentmon, kiln-front-end, font-pick, dinov3; close them with decisions in that session).
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

